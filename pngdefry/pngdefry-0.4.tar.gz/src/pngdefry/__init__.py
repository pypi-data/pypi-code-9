import argparse
import tempfile

import _pngdefry


__all__ = ['decode', 'decode_content', 'InputFileError',
           'NotIPhoneCompressedError']


class InputFileError(Exception):
    pass


def decode(input_file, output_file=None):
    """
    Removes PNG image optimizations specific to the iOS platform.
    :param input_file: Input PNG filename.
    :param output_file: Output filename
    :return: Path to the output file. If `input_file` was not iPhone
    optimized (and input file is a valid PNG) this method will return
    `input_file`
    """
    output_file = output_file or tempfile.mktemp()
    ret_val = _pngdefry.process(input_file, output_file)

    if ret_val == 2:
        # Input PNG file was not iPhone optimized. Return the input file as
        # the result.
        return input_file
    elif ret_val != 1:
        raise InputFileError("Not a PNG: {0}".format(input_file))

    return output_file


def decode_content(content):
    """
    Process input image `content` with the `decode` method.
    This function creates two temporary files while processing input data.

    :param content: Input PNG image file bytes
    :return: Processed image content
    """
    with tempfile.NamedTemporaryFile() as in_tmp:
        in_tmp.write(content)
        in_tmp.flush()

        with tempfile.NamedTemporaryFile() as out_tmp:
            output_file_path = decode(in_tmp.name, out_tmp.name)

            if output_file_path == in_tmp.name:
                # Input file was not iPhone optimized. Input=Output
                out = in_tmp
            else:
                # File was fully processed. Return output content
                out = out_tmp

            out.seek(0)
            return out.read()



def main():
    parser = argparse.ArgumentParser('Pngdefry CLI')
    parser.add_argument('input', help='Input PNG file')
    parser.add_argument('-o', '--output', help='Output file')
    args = parser.parse_args()

    try:
        output = decode(args.input, args.output)
    except InputFileError, e:
        print(e)
        return

    print("{0} processed".format(args.input))
    print("Output: {0}".format(output))

if __name__ == '__main__':
    main()
