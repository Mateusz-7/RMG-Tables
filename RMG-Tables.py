from GoogleMyMaps import GoogleMyMaps

map_link = 'https://www.google.com/maps/d/u/0/edit?mid=1QU5ydDpF5bg_8jfQca3An2qJfqddpcY&usp=sharing'


if __name__ == '__main__':
    gmm = GoogleMyMaps()
    my_map = gmm.create_map(map_link)
    print(my_map)
