// const keywords = {
//     'tags' : [],
//     'skin_type': '',
//     'importance' : ''
// };

// function selectOptions(className, value) {
// f (!keywords[className]) {
//         keywords[className] = check ? [value] : value;
//     }else {
//         if (check) {
//             keywords[className].push(value);
//         } else {
//             keywords[className] = value;
//             console.log(keywords[className]);
//         }
//     }
// }
// function selectImportance() {
//     const ImportanceRadios = document.querySelectorAll('.importance input[type="radio"]');
    
//     ImportanceRadios.forEach(radio => {
//         if (radio.checked) {
//             keywords['importance'] = radio.nextElementSibling.textContent.trim();
//         }
//     });
// }

// function selectTags() {
//     const tagCheckboxes = document.querySelectorAll('.tags input[type="checkbox"]');
    
//     keywords['tags'] = [];

//     tagCheckboxes.forEach(checkbox => {
//         if (checkbox.checked) {
//             keywords['tags'].push(checkbox.nextElementSibling.textContent.trim());
//         }
//     });
// }
// const data = document.querySelector('input[name="skin_type"]:checked').value;

// console.log(data);
//     const check = className === 'tags';

const keywords = {
    'tags' : [],
    'skin_type': '',
    'importance' : ''
};

function submitFunction() {
    const keywords = {
        'tags': [],
        'skin_type': '',
        'importance': ''
    };
    // skin_type : 피부 타입
    const skinTypeRadio = document.querySelector('input[name="skin_type"]:checked');
    if (skinTypeRadio) {
        keywords.skin_type = skinTypeRadio.value;
    }
    
    // importance : 가장 중요한 요소
    const importanceRadio = document.querySelector('input[name="skin_tone"]:checked');
    if (importanceRadio) {
        keywords.importance = importanceRadio.value;
    }
    // tags : 피부 고민
    const selectedTagCheckboxes = document.querySelectorAll('input[name="skin_troube"]:checked');
    selectedTagCheckboxes.forEach(checkbox => {
        keywords.tags.push(checkbox.value);
    });

    console.log('keywords:', keywords);
    
    fetch('/user_keywords', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(keywords)
    })
    .catch (error => {
        console.log('error', error);
    });
}

// tags, skin_type, importance

// const data = document.querySelector('input[name="skin_type"]:checked').value;
// console.log('data',data);

// const impot = document.querySelector('input[name="skin_tone"]:checked').value;
// console.log('data',impot);

const tag = document.querySelector('input[name="skin_troube"]:checked').value;
console.log('data',tag);