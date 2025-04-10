from GoogleMyMaps import GoogleMyMaps

map_link = 'https://www.google.com/maps/d/u/0/edit?mid=1QU5ydDpF5bg_8jfQca3An2qJfqddpcY&usp=sharing'

# TODO: add exception handling for problems with Map
if __name__ == '__main__':
    gmm = GoogleMyMaps()
    google_map = gmm.create_map(map_link)
    print(google_map)
    # print([layer.name for layer in google_map.layers])
    
    # 1: generate list of obstacles
    # 2: add graphic interface
    # 3: ensure compatibility across different operating systems
    # 4: add more features (kilometers, person assigned)

    # TODO: Tkinter -> save file where user wants
