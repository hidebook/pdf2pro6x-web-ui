import sys
from pdf2pro6x import main as convert_pdf

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python converter.py <input.pdf> <output.pro6x>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_pro6x = sys.argv[2]

    convert_pdf(input_pdf, output_pro6x)
