import os


def check_for_pdf(path):
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1] == ".pdf":
            return True
    return False


def count_pdfs_in_path(path):
    pdf_count = 0
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1] == ".pdf":
            pdf_count += 1
    return pdf_count
