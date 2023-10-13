function loadJson(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
}


function init() {
    var jsonData = loadJson('#jsonData');

    var lat = jsonData.map((item) => item.lat);
    var lon = jsonData.map((item) => item.lon);

    let map = new ymaps.Map('map', {
        center: [lat, lon],
        zoom: 15
    });

    let placemark = new ymaps.Placemark([lat, lon], {
        balloonContentHeader: 'Эконом Сити',
        balloonContentBody: 'ул. Долгобродская, 3',
        balloonContentFooter: '+375(29)803-21-68',
        },{
        iconLayout: 'default#image', // указали, что будем использовать свой стиль для метки
        iconImageHref: 'static/img/map-point.png', // используем выбранный нами стиль метки
        iconImageSize: [30, 30], // используем выбранный нами стиль метки
        iconImageOffset: [-14, -25], // отступ от центра
        });

    map.controls.remove('geolocationControl');  // удаляем геолокацию
    map.controls.remove('searchControl');  // удаляем поиск
    map.controls.remove('trafficControl');  // удаляем контроль трафика
    map.controls.remove('typeSelector');  // удаляем тип
    // map.controls.remove('fullscreenControl');  // удаляем кнопку перехода в полноэкранный режим
    // map.controls.remove('zoomControl');  // удаляем контрол зумирования
    // map.controls.remove('rulerControl');  // удаляем линейку
    map.controls.remove(['scrollZoom']);  // отключаем скролл карты (опционально)

    map.geoObjects.add(placemark);
}


ymaps.ready(init);