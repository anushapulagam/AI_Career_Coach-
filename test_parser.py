from modules.resume_parser import get_resume_text

text = get_resume_text("resume.pdf")

print("✅ Resume extracted successfully!")
print("-" * 50)
print(text)
print("-" * 50)
print(f"Total characters: {len(text)}")