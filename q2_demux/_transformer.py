import shutil

from q2_types.per_sample_sequences import FastqGzFormat

from .plugin_setup import plugin
from ._demux import BarcodeSequenceIterator, _read_fastq_seqs
from ._format import EMPMultiplexedDirFmt, EMPMultiplexedSingleEndDirFmt


@plugin.register_transformer
def _1(dirfmt: EMPMultiplexedDirFmt) -> BarcodeSequenceIterator:
    barcode_generator = _read_fastq_seqs(
        str(dirfmt.barcodes.view(FastqGzFormat).path))
    sequence_generator = _read_fastq_seqs(
        str(dirfmt.sequences.view(FastqGzFormat).path))
    result = BarcodeSequenceIterator(barcode_generator, sequence_generator)
    # ensure that dirfmt stays in scope as long as result does so these
    # generators will work.
    result.__dirfmt = dirfmt
    return result


@plugin.register_transformer
def _2(dirfmt: EMPMultiplexedSingleEndDirFmt) -> EMPMultiplexedDirFmt:
    # TODO: revisit this API to simpify defining transformers
    result = EMPMultiplexedDirFmt().path

    sequences_fp = str(result / 'sequences.fastq.gz')
    barcodes_fp = str(result / 'barcodes.fastq.gz')
    shutil.copyfile(str(dirfmt.sequences.view(FastqGzFormat)), sequences_fp)
    shutil.copyfile(str(dirfmt.barcodes.view(FastqGzFormat)), barcodes_fp)

    return result
