const addressInput = document.getElementById("address");
const addressOptions = {
    fields: ["formatted_address", "geometry", "name"],
    strictBounds: false,
    types: ["geocode"],
  };
const addressAutocomplete = new google.maps.places.Autocomplete(addressInput, addressOptions);
const addressInfowindow = new google.maps.InfoWindow();
addressAutocomplete.addListener("place_changed", () => {
    addressInfowindow.close();
    const place = addressAutocomplete.getPlace();
    if (!place.geometry || !place.geometry.location) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            document.getElementById("address").innerText = ""
            return;
        }

        // console.log(place)
        console.log(place.geometry.location.lat())
        console.log(place.formatted_address)
        document.getElementById("latitude").value = place.geometry.location.lat()
        document.getElementById("longitude").value = place.geometry.location.lng()
    
  })