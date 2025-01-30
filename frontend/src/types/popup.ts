interface ApartmentInfo{
    apartment: string,
    price: number
}

interface ApartmentPopup{
    longitude: number,
    latitude: number,
    house: string,
    apartments: Array<ApartmentInfo>

}


export type {ApartmentPopup, ApartmentInfo};