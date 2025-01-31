import imageio.v2 as imageio
import numpy as np

#funcionIsBlackandWhite
def is_blackAndWhite(img_array):
    # Zkontroluj, jestli je obrázek dvourozměrný (grayscale)
    if len(img_array.shape) == 2:
        return True

    # Zkontroluj, jestli ulozen jako RGB, ale je cernobily tzn vsechny kanaly maji stejne hodnoty
    if img_array.shape[2] == 3:
        if np.all(img_array[:, :, 0] == img_array[:, :, 1]) and np.all(img_array[:, :, 1] == img_array[:, :, 2]):
            print("Obrázek je černobílý (ale je ve formátu RGB).")
            return True

    return False  # Pokud není černobílý

#functionReturnToNegativ
def convert_to_negativ(img_array):
    return 255 - img_array


#lighter
def convert_to_lighter(img_array, percentage):
    # Vypočti zvýšení o dané procento
    increase = img_array * percentage

    # Přidej zvýšení k původní hodnotě a omez hodnoty na max 255
    lightened = np.clip(img_array + increase, 0, 255)

    return lightened.astype(np.uint8)

#darker
def convert_to_darker(img_array, percentage=0.5):
    # Vypočti zvýšení o dané procento
    increase = img_array * percentage

    # Přidej zvýšení k původní hodnotě a omez hodnoty na max 255
    darkened = np.clip(img_array - increase, 0, 255)

    return darkened.astype(np.uint8)
#smallerPicture
def make_smaller(img_array):
    if(is_blackAndWhite(img_array)):
        return img_array[::2, ::2] #cernobily vyber kazdy druhy radek a sloupec a prumer z nich
    else:
        red_channel = img_array[::2, ::2, 0] #::2 neni specifikovan zacatek ani konec ale vybura kazdy druhy prvek
        green_channel = img_array[::2, ::2, 1]
        blue_channel = img_array[::2, ::2, 2]

        colors_together = np.stack([red_channel, green_channel, blue_channel], axis=-1) #np.stack() funkce na spojeni vice poli
                                                                                                # Osa, podél které se pole spojí. axis=-1 znamená, že se pole přidají jako nová poslední dimenze
        return colors_together
#pictureImport
img_array = imageio.imread('C:/Users/ivagi/PycharmProjects/Seminarka/stene_barevne.jpg')
print('puvodni obrazek:',  img_array.shape)

if is_blackAndWhite(img_array):
    print("Obrazek je cernobily")
else:
    print("Obrazek je barevny")

#createNegativ
negative_picture = convert_to_negativ(img_array)

#SaveNewPictureNegativ
output_path1 = 'C:/Users/ivagi/PycharmProjects/Seminarka/negative_stene_barevne.jpg'
imageio.imwrite(output_path1, negative_picture)
print('negativ :',  negative_picture.shape)

#SaveNewLighterPicture
lighter_picture = convert_to_lighter(img_array)
output_path2 = 'C:/Users/ivagi/PycharmProjects/Seminarka/lighter_stene_barevne.jpg'
imageio.imwrite(output_path2, lighter_picture)

#SaveNewDarkerPicture
darker_picture = convert_to_darker(img_array)
output_path3 = 'C:/Users/ivagi/PycharmProjects/Seminarka/darker_stene_barevne.jpg'
imageio.imwrite(output_path3, darker_picture)

#SaveNewSmallerPicture
smaller_picture = make_smaller(img_array)
output_path4 = 'C:/Users/ivagi/PycharmProjects/Seminarka/smaller_stene_barevne.jpg'
imageio.imwrite(output_path4, smaller_picture)
