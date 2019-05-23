import trafaret as t


PRODUCT_ADD = t.Dict({
    'name': t.String(),
    'price': t.Int(),
})
