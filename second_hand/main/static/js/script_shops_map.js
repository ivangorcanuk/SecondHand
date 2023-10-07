const categoriesData = {
    category1: [{
            lat: 53.9202155706571,
            lon: 27.57452449999998,
            name: 'Мода Макс'
        },
        {
            lat: 53.924654070639384,
            lon: 27.591547499999912,
            name: 'Мода Макс'
        },
        {
            lat: 53.92518907064077,
            lon: 27.607186999999957,
            name: 'Мода Макс'
        }
    ],
    category2: [{
            lat: 53.90329157067195,
            lon: 27.546281499999957,
            name: 'Эконом Сити'
        },
        {
            lat: 53.90167357066778,
            lon: 27.602380999999962,
            name: 'Эконом Сити'
        },
        {
            lat: 53.91784557065102,
            lon: 27.58914899999998,
            name: 'Эконом Сити'
        }
    ],
    category3: [{
            lat: 53.88545307065526,
            lon: 27.503835999999996,
            name: 'Адзенне'
        },
        {
            lat: 53.91822207062285,
            lon: 27.45385349999998,
            name: 'Адзенне'
        },
        {
            lat: 53.939317070618756,
            lon: 27.59462850000001,
            name: 'Адзенне'
        }
    ],
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
                hintContent: item.name,
                balloonContent: item.name,
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