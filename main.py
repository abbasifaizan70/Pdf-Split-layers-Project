from PDFNetPython3.PDFNetPython import PDFDoc, Context, PDFDraw, Group, PDFNet
from pathlib import Path

PDFNet.Initialize("demo:1633616420220:78ad5199030000000030f5b54c476332249c67b5ffa2d5c8409e6352c1")


def split_pdf_into_layers(file_path, save_path):
    """
    split
    :param file_path:
    :param save_path:
    :return:
    """
    file_save_path_prefix = Path(save_path, Path(file_path).stem)
    doc = PDFDoc(file_path)

    page = doc.GetPage(1)

    init_cfg = doc.GetOCGConfig()
    ctx = Context(init_cfg)

    pdfdraw = PDFDraw()
    pdfdraw.SetImageSize(int(page.GetPageWidth()), int(page.GetPageWidth()))
    pdfdraw.SetOCGContext(ctx)  # Render the page using the given OCG context.

    # Disable drawing of content that is not optional (i.e. is not part of any layer).
    ctx.SetNonOCDrawing(False)

    # Now render each layer in the input document to a separate image.
    ocgs = doc.GetOCGs()  # Get the array of all OCGs in the document.
    total_ocgs = ocgs.Size()
    current_ocg_number = 0
    while current_ocg_number < total_ocgs:
        ocg = Group(ocgs.GetAt(current_ocg_number))
        ctx.ResetStates(False)
        ctx.SetState(ocg, True)
        file_name = "{prefix_path}-{layer_name}.png".format(prefix_path=file_save_path_prefix, layer_name=ocg.GetName())
        pdfdraw.Export(page, file_name)
        current_ocg_number = current_ocg_number + 1


# change your username below
split_pdf_into_layers(
    file_path='D-BAYLOR-2021-GONZAGA.pdf',
    save_path='/Users/abbas/Downloads/python_pdf_ocg_layers/layers'
)

