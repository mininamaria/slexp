// Создание обработчика для события window.onLoad
YMaps.jQuery(function () {
    // Создание экземпляра карты и его привязка к созданному контейнеру
    var map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);

    // Установка для карты ее центра и масштаба
    map.setCenter(new YMaps.GeoPoint(43.998779,56.316537), 13);

	map.addControl(new YMaps.Zoom());
	map.addControl(new YMaps.TypeControl());
	map.addControl(new YMaps.ToolBar());

    // Создание и добавление YMapsML-документа на карту
    var ml = new YMaps.YMapsML("https://github.com/mininamaria/slexp/blob/main/YMapsML.xml");
    map.addOverlay(ml);

    // Обработчик неудачной загрузки YMapsML
    YMaps.Events.observe(ml, ml.Events.Fault, function (ml, error) {
        alert('Ошибка: ' + error);
    });
});
