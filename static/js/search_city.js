$('#city_form').select2({
    minimumInputLength: 3,
    ajax: {
        url: '/openweathermap/api/cities',
        delay: 300,
        cache: true,
        data: function (params) {
            var query = {
                name: params.term
            }
            return query
        },
        processResults: function (data) {
            let newData = []
            $.each(data.cities, function (i, d) {
                let city_fullname = [d.local_name, d.country]
                newData.push({id: d.id, text: city_fullname.join(", "), latitude: d.lat, longitude: d.lon})
            })
            return {
                results: newData
            }
        }
    }
})

$('#city_form').on('select2:select', function (e) {
    var data = e.params.data
    $('#latitude_form').val(data.latitude)
    $('#longitude_form').val(data.longitude)
})
