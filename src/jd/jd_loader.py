# src/jd/jd_loader.py

from docx import Document


def load_jd(filepath):

    doc = Document(filepath)

    text = []

    for para in doc.paragraphs:
        text.append(para.text)

    return "\n".join(text)


if __name__ == "__main__":

    jd = load_jd(
        "data/job_description.docx"
    )

    print("\n===== JOB DESCRIPTION =====\n")

    print(jd[:5000])