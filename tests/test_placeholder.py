from translator.placeholders import PlaceholderProtector

p = PlaceholderProtector()

text = "Customer {0} has %(count)d invoices\\n<b>OK</b>"

protected, mapping = p.protect(text)

print("Protected:")
print(protected)
print()

restored = p.restore(protected, mapping)

print("Restored:")
print(restored)
print()

print("Valid:", p.validate(text, restored))