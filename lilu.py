class DasaX:
    a = 10
    b = 20

    def t1(self, f1):
        print("{} haha {}".format(self.a, f1))

    def t2(self, f1):
        print("{} mumu {}".format(self.b, f1))



def find():
    a = fromstring(x.text)

    w = a.xpath("//blockquote")
    for element1 in w:
        g = element1.xpath("//p")
        for element2 in g:
            print(element2.text)