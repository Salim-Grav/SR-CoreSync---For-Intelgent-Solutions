import io
c = io.open("en/index.html", encoding="utf-8").read()
i = c.find('class="form-cta"')
print(repr(c[i-150:i+700]))
