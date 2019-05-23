import trafaret as t


ORDER_ADD = t.Dict({
    'user_id': t.Int(),
    'product_ids': t.List(t.Int())
})
