function uploadImage() {
    const fileInput = document.getElementById('fileInput');
    fileInput.click();
}

document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function(readerEvent) {
        const imageDataUrl = readerEvent.target.result;
        const uploadedImage = document.getElementById('uploadedImage');
        uploadedImage.src = imageDataUrl;
    };

    reader.readAsDataURL(file);
});

// 이미지 파일, 닉네임을 입력받아 formdata에 저장해주고 서버로 전송
// 전송이 완료되면 result 페이지로 넘어간다.
function sendImageToBackend() {
    const file = document.getElementById('fileInput').files[0];
    const nickname = document.getElementById('nickname').value;
    // const file = fileInput.files[0];

    const formData = new FormData();
    formData.append('image', file);
    formData.append('nickname', nickname);

    fetch('/second', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            console.log('이미지 업로드 성공');
            console.log(data);
            // 여기에서 다음 동작 또는 페이지 전환 로직을 추가하세요
            window.location.href = '/result';
        })
        .catch(error => {
            console.log('이미지 업로드 오류:', error);
        });
}
