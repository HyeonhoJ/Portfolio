// async function postData(url = "", data = {}) {
//     // Default options are marked with *
//     const response = await fetch(url, {
//     method: "POST", // *GET, POST, PUT, DELETE, etc.
//     mode: "cors", // no-cors, *cors, same-origin
//     cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
//     // credentials: "same-origin", // include, *same-origin, omit
//     headers: {
//         "Content-Type": "application/json",
//         // 'Content-Type': 'application/x-www-form-urlencoded',
//     },
//     redirect: "follow", // manual, *follow, error
//     referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
//     body: JSON.stringify(data), // body data type must match "Content-Type" header
//     });

//     return response.json(); // parses JSON response into native JavaScript objects
// }

// function updateImageElements(data) {
//     innerBoxes = document.getElementsByClassName("inner_box");
//     for(let i = 0; i < innerBoxes.length; i++) {
//         innerBoxes[i].childNodes[1].childNodes[1].src = data[i].imgSrc;
//     }
// }

// function updateDetailElements(data) {
//     details = document.getElementsByClassName("detail");
//     for(let i = 0; i < details.length; i++) {
//         brand = details[i].childNodes[1];
//         brand.innerHTML = data[i].brand;

//         item_name = details[i].childNodes[3];
//         item_name.innerHTML = data[i].item_name;

//         color = details[i].childNodes[5];
//         color.innerHTML = data[i].color;
        
//         price = details[i].childNodes[7];
//         price.innerHTML = data[i].price;
//     }
// }

// function showItems(item_type) {
//     postData("/iteminfo", {"item_type": item_type})
//     .then((data) => {
//         updateDetailElements(data);
//         updateImageElements(data); 
//     });
// }

// window.onload = () => {
//     showItems("lip");
// };

// async function postData(url='', data={}) {
//     // Default options are marked with *
//     const response = await fetch(url, {
//     method: "POST", // *GET, POST, PUT, DELETE, etc.
//     mode: "cors", // no-cors, *cors, same-origin
//     cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
//     // credentials: "same-origin", // include, *same-origin, omit
//     headers: {
//         "Content-Type": "application/json",
//         // 'Content-Type': 'application/x-www-form-urlencoded',
//     },
//     redirect: "follow", // manual, *follow, error
//     referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
//     body: JSON.stringify(data), // body data type must match "Content-Type" header
//     });
    
//     return response.json(); // parses JSON response into native JavaScript objects
// }

// document.addEventListener('DOMContentLoaded', function () {

//     const nickname = sessionStorage.getItem('nickname');

//     if (nickname) {
//         document.getElementById('nickname').innerText = nickname + '님을 위한 추천 상품';
//     } else {
//         document.getElementById('nickname').innerText = '당신을 위한 추천 상품';
//     }
// });

// function updateImageElements(data) {
//     innerBoxes = document.getElementsByClassName("inner_box");
//     for(let i = 0; i < innerBoxes.length; i++) {
//         innerBoxes[i].querySelector('.item_box img').src = data[i].imgSrc;
//     }
// }


// function updateDetailElements(data) {
//     details = document.getElementsByClassName("detail");
//     for(let i = 0; i < details.length; i++) {
//         details[i].querySelector('.brand').innerHTML = data[i].brand;
//         details[i].querySelector('.item_name').innerHTML = data[i].item_name;
//         details[i].querySelector('.color').innerHTML = data[i].color;
//         details[i].querySelector('.price').innerHTML = data[i].price;
//     }
// }


// window.onload = () => {
//     showItems("lip");
// };

// // 사용자의 닉네임 가져오기 위한 함수, 메서드
// async function fetchNicknameFromServer() {
//     const response = await fetch('/get_nickname', {
//         method: 'GET',
//         mode: 'cors',
//         cache: 'no-cache',
//         credentials: 'same-origin',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         redirect: 'follow',
//         referrerPolicy: 'no-referrer'
//     });

//     return response.json();
// }

// document.addEventListener('DOMContentLoaded', function () {
//     // Fetch nickname from the server
//     fetchNicknameFromServer()
//         .then((data) => {
//             const nickname = data.nickname;
//             if (nickname) {
//                 document.getElementById('nickname').innerText = nickname + '님을 위한 추천 상품';
//                 // Store nickname in sessionStorage for future use
//                 sessionStorage.setItem('nickname', nickname);
//             } else {
//                 document.getElementById('nickname').innerText = '사용자님을 위한 추천 상품';
//             }
//         })
//         .catch((error) => {
//             console.error('Error fetching nickname:', error);
//         });
// });

// result.html, content_based.html 에서의 파라미터로 
// 3개를 나눴으니 이렇게 불러온다.
// const recommendation_plus = ''
// const recommendation_less = ''
// const recommendation_skin = ''
// document.addEventListener('DOMContentLoaded', function() {
//     const queryString = window.location.search;
//     const urlParams = new URLSearchParams(queryString);
//     const recommendationType = urlParams.get('recommendation_type')

//     fetch(`/get_recommendation?type=${recommendationType}`)
//         .then(response => response.json())
//         .then(data => {
//             console.log(data);
//         })
//         .catch(error=> {
//             console.error(error);
//         })
// })

// 최초 페이지 lip
// document.addEventListener('DOMContentLoaded', function() {
//     showItems('lip');
// });

function showItems(category) {
    // const nextPageURL = '/final_page?' + dataParam;
    // window.location.href = nextPageURL;
    
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const recommendType = urlParams.get('recommend_type')

    let dataParam;

    if(category === 'lip') {
        dataParam = 'lip';
    } else if(category === 'eyeshadow') {
        dataParam = 'eyeshadow';
    } else if(category === 'blusher') {
        dataParam = 'blusher';
    }

    const nextPageURL = `/final_page?cosmetic_type=${encodeURIComponent(dataParam)}&recommend_type=${encodeURIComponent(recommendType)}`;
    window.location.href = nextPageURL;
}



