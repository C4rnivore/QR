from QrEncoder import encode
from QrService import add_service, fill_qr, split_by_blocks, create_correction, combine_blocks_with_correction, get_qr_version
from QrDrawer import draw_qr

out = encode('HTTP/132131HTTPS://HABR.COM/RU/132131HTTPS://HABR.COM/RU/132131HTTPS://HABR.CO32131HTTPS://HABR.COM/RU/132131HTTPS://HABR.COM32131HTTPS://HABR.COM/RU/132131HTTPS://HABR.COM32131HTTPS://HABR.COM/RU/132131HTTPS://HABR.COMM/RU/132131')



service = add_service(out)
fill = fill_qr(service)
block = split_by_blocks(fill)
correction_list = create_correction(block)
flow = combine_blocks_with_correction(correction_list)


draw_qr(get_qr_version(), flow)





