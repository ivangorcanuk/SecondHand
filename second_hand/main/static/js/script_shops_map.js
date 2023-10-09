function loadJson(selector) {
    return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
}

const categoriesData = {
    category1: loadJson('#jsonData')[0],
    category2: loadJson('#jsonData')[1],
    category3: loadJson('#jsonData')[2],
    category4: loadJson('#jsonData')[3],
    category5: loadJson('#jsonData')[4],
}

const init = () => {
    let map = new ymaps.Map('map-shops', {
        center: [53.907992125707025,27.557558236816423],
        zoom: 11
    });

    let activeCategory = 'category1';

    const showCategory = (category) => {
        map.geoObjects.removeAll(); // удаляем все маркеры с карты

        categoriesData[category].forEach((item) => { // проходим циклом по славарю с координатами
            const placemark = new ymaps.Placemark([item.lat, item.lon], {
                balloonContentHeader: item.name,
                balloonContentBody: item.address,
                balloonContentFooter: item.number_phone,
            },{
                iconLayout: 'default#image', // указали, что будем использовать свой стиль для метки
                iconImageHref: 'static/img/map-point.png', // используем выбранный нами стиль метки
                iconImageSize: [30, 30], // установили размер метки
                iconImageOffset: [-15, 30], // отступ от центра
            });

            map.geoObjects.add(placemark); // удаляем все маркеры с карты
        });

        activeCategory = category;
    }
    const categoryButtons = document.querySelectorAll('.category-button');
    categoryButtons.forEach((button) => {
        button.addEventListener('click', (e) => {
            const category = e.currentTarget.dataset.category;
            showCategory(category)
        });
    });

    showCategory(activeCategory)
};


ymaps.ready(init);