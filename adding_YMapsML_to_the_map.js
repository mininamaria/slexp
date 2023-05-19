ymaps.ready(init);

function init () {
    // Создание экземпляра карты.
    var myMap = new ymaps.Map('map', {
            center: [61.678423, 96.377965],
            zoom: 2
        }, {
            searchControlProvider: 'yandex#search'
        });

    // Загрузка YMapsML-файла.
    ymaps.geoXml.load('draft.xml')
        .then(function (res) {
            // Добавление геообъектов на карту.
            myMap.geoObjects.add(res.geoObjects);
           // Вызывается в случае неудачной загрузки YMapsML-файла.
        }, function (error){
            alert('Ошибка: ' + error);
        });
}
