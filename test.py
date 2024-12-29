from django.utils.text import slugify

print("test")

input_string = "Django Store App...Simplicity at it's finest."

output_string = slugify(input_string)

print(input_string)
print(output_string)
