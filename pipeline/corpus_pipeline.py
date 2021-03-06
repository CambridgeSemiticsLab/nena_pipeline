import re
import json
import collections
import traceback
from pathlib import Path
import unicodedata as ucd
from tf.client.make.build import makeSearchClients
from .nena_parser import NenaLexerParser
from .build_tf import NenaTfBuilder
from .build_docs import DocsBuilder

class CorpusPipeline:

    def __init__(self, configs):

        """Initialize pipeline configs / error handling.

        Args:
            configs: string or dict. If string, should be a
                filepath to a json file of configs. If dict,
                should contain all of the necessary config
                keys for the parser processes.
        """

        # load and set up configs
        if type(configs) == str:
            with open(configs, 'r') as infile:
                self.configs = json.load(infile)
        elif type(configs) == dict:
            self.configs = configs
        else:
            raise Exception(
                '"configs" should be either string (filepath) '
                 f'or dict, not {type(configs)}'
            )

        # a place to store error messages;
        # the messages are keyed by process,
        # the value is a list of error strings
        self.errors = {}

    def get_traceback(self, error):
        """Format error traceback into string.

        source:
        https://stackoverflow.com/questions/62952273/
        how-to-catch-python-exception-and-save-traceback-text-as-string
        """
        return ''.join(
            traceback.format_exception(
                None, error, error.__traceback__
            )
        )

    def build_corpus(self, indir, outdir):
        """Parse and index (TF) the nena corpus.

        Args:
            indir: a directory containing .nena markup files
            outdir: a directory to contain the output of the pipeline

        Returns:
            Exports to the outdir three things:
                1) `tf` directory containing the indexed corpus in
                    text-fabric format
                2) documentation.md: a file containing documentation
                    on the makeup of the corpus
                3) search_tool: set of static files which are the
                    nena_search compiled from the corpus data
        """

        # create the outdir if needed
        if not Path(outdir).exists():
            Path(outdir).mkdir()

        # parse the .nena files
        dialect2data = self.parse_nena(indir)

        # index the data with Text-Fabric;
        # produces .tf files
        self.build_tf(dialect2data, outdir)

        # build docs
        self.build_docs(outdir)

        # build search tool
        self.build_layered_search(outdir)

    def parse_nena(self, inpath):
        """Parse .nena markup files."""

        # set up NENA markup lexer and parser
        lexer, parser = NenaLexerParser(self.configs)

        # instantiate error list
        errlog = self.errors['nena_parser'] = []

        # load .nena files
        textdir = Path(inpath)
        _dialect2data_ = collections.defaultdict(list)

        # -- Attempt to parse each text --

        print('Beginning parsing of NENA formatted texts...')
        for textfile in sorted(textdir.glob('*.nena')):
            read_text = textfile.read_text()
            norm_text = ucd.normalize('NFD', read_text) # norm to decomposed chars
            metadata = self.get_metadata(norm_text)

            try:
                corpus_id = metadata['corpus_id']
            except KeyError:
                errlog.append(
                    f'File {textfile} does not have `corpus_id` metadata!'
                )

            # attempt to parse the text
            # if parse fails, save message to the error log referenced by the corpus_id
            try:
                print(f'\tparsing {textfile}...')
                parsed = parser.parse(
                    lexer.tokenize(norm_text)
                )
            except Exception as e:
                print(f'\t\tfail')
                traceback = self.get_traceback(e)
                errlog.append(f'corpus_id {corpus_id}: {traceback}')
                continue

            metadata, text = parsed
            dialect = metadata['dialect']
            _dialect2data_[dialect].append(parsed) # parse mapped to dialect
        print('DONE parsing all .nena texts!')

        # -------

        # ensure that dialects are sorted alphabetically, because
        # the index made by TF will model whatever order it is fed
        dialect2data = collections.OrderedDict()
        for dialect in sorted(_dialect2data_):
            dialect2data[dialect] = _dialect2data_[dialect]

        return dialect2data

    def get_metadata(self, nenastring):
        """Retrieve metadata from a .nena markdown string.

        Though metadata is parsed in the parser,
        we need a "dumb" way to get metadata from a file
        before it is parsed so that parse errors can be tied to
        corpus_id rather than just a filename.
        """
        meta_re = r'([^\s]*)\s*::\s*([^\s]*)'
        metadata = dict(re.findall(meta_re, nenastring))
        return metadata

    def build_tf(self, dialect2data, outdir):
        """Index the parsed .nena data into a Text-Fabric resource."""
        # instance an error list
        errlog = self.errors['tf_builder'] = []
        try:
            print()
            print('Indexing new corpus data...')
            tfbuilder = NenaTfBuilder(
                dialect2data,
                outdir,
                self.configs,
            )
            tfbuilder.build()
            print('\tSUCCESS! TF corpus built.')
        except Exception as e:
            traceback = self.get_traceback(e)
            errlog.append(f'TEXT FABRIC INDEXING FAILED; REASON: {traceback}')

    def build_docs(self, outdir):
        """Automatically build documentation on the corpus."""
        print()
        print('Loading TF data and building documentation...')
        docs_builder = DocsBuilder(self.configs, outdir)
        docs_builder.compile_doc()
        print('\tdone!')

    def build_layered_search(self, outdir):
        """Build layered search tool from TF files."""
        print()
        print('Building search tool...')
        search_dir = Path(outdir).joinpath('search_tool')
        tf_dir = Path(outdir).joinpath('tf')
        makeSearchClients(
            'nena',
            str(search_dir),
            self.configs['search_configs'],
            dataDir=str(tf_dir)
        )
        print('\tdone!')
