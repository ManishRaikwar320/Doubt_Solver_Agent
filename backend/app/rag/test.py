from retriever import index_image, retrieve_context

img_path = r"D:\Downloads\1. DESKTOP\Projects\4. AI Agents project\Doubt Solver Bot\data\uploads\demo.png"

# Apni actual image ka path dein.
result = index_image(
    image_path=img_path,
    source_id="physics_chapter_1",
)

print("Chunks created:", result["chunks_created"])
print("Extracted text:", result["text"])


# Ab us page se question poochhein.
answer_context = retrieve_context(
    question="Explain Newton's second law with an example.",
    k=4,
)

print("\nRetrieved context:")
print(answer_context["context"])

print("\nSources:")
print(answer_context["sources"])
