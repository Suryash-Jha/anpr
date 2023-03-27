
$(document).ready(function () {
	var inputs = document.querySelectorAll('.inputfile');
	Array.prototype.forEach.call(inputs, function (input) {
		var label = input.nextElementSibling,
			labelVal = label.innerHTML;

		input.addEventListener('change', function (e) {
			var fileName = '';
			if (this.files && this.files.length > 1)
				fileName = (this.getAttribute('data-multiple-caption') || '').replace('{count}', this.files.length);
			else
				fileName = e.target.value.split('\\').pop();

			if (fileName) {
				label.querySelector('span').innerHTML = fileName;

				let reader = new FileReader();
				reader.onload = function () {
					let dataURL = reader.result;
					$("#selected-image").attr("src", dataURL);
					$("#selected-image").addClass("col-12");
				}
				let file = this.files[0];
				reader.readAsDataURL(file);
				startRecognize(file);
			}
			else {
				label.innerHTML = labelVal;
				$("#selected-image").attr("src", '');
				$("#selected-image").removeClass("col-12");
				$("#arrow-right").addClass("fa-arrow-right");
				$("#arrow-right").removeClass("fa-check");
				$("#arrow-right").removeClass("fa-spinner fa-spin");
				$("#arrow-down").addClass("fa-arrow-down");
				$("#arrow-down").removeClass("fa-check");
				$("#arrow-down").removeClass("fa-spinner fa-spin");
				$("#log").empty();
			}
		});

		// Firefox bug fix
		input.addEventListener('focus', function () { input.classList.add('has-focus'); });
		input.addEventListener('blur', function () { input.classList.remove('has-focus'); });
	});
});

$("#startLink").click(function () {
	var img = document.getElementById('selected-image');
	startRecognize(img);
});

function startRecognize(img) {
	$("#arrow-right").removeClass("fa-arrow-right");
	$("#arrow-right").addClass("fa-spinner fa-spin");
	$("#arrow-down").removeClass("fa-arrow-down");
	$("#arrow-down").addClass("fa-spinner fa-spin");
	recognizeFile(img);
}

// function progressUpdate(packet) {
// 	var log = document.getElementById('log');

// 	if (log.firstChild && log.firstChild.status === packet.status) {
// 		if ('progress' in packet) {
// 			var progress = log.firstChild.querySelector('progress')
// 			progress.value = packet.progress
// 		}
// 	} else {
// 		var line = document.createElement('div');
// 		line.status = packet.status;
// 		var status = document.createElement('div')
// 		status.className = 'status'
// 		// status.appendChild(document.createTextNode(packet.status))
// 		// line.appendChild(status)

// 		if ('progress' in packet) {
// 			var progress = document.createElement('progress')
// 			progress.value = packet.progress
// 			progress.max = 1
// 			// line.appendChild(progress)
// 		}


// 		if (packet.status == 'done') {
// 			log.innerHTML = ''
// 			var pre = document.createElement('pre')
// 			pre.appendChild(document.createTextNode(packet.data.text.replace(/\n\s*\n/g, '\n')))
// 			line.innerHTML = ''
// 			line.appendChild(pre)
// 			$(".fas").removeClass('fa-spinner fa-spin')
// 			$(".fas").addClass('fa-check')
// 		}

// 		log.insertBefore(line, log.firstChild)
// 	}
// }


function cleanResult(text) {
	var res = '';
	for (var i = 0; i < text.length; i++) {
		if ((text[i].charCodeAt(0) >= 65 && text[i].charCodeAt(0) <= 90) || (text[i].charCodeAt(0) >= 97 && text[i].charCodeAt(0) <= 122) || (text[i].charCodeAt(0) >= 48 && text[i].charCodeAt(0) <= 57)) {
			res += text[i];
		}
		// else console.log(text[i]);

	}
	// console.log(res);
	return res;
}
function recognizeFile(file) {
	$("#log").empty();
	const corePath = window.navigator.userAgent.indexOf("Edge") > -1
		? 'static/js/tesseract-core.asm.js'
		: 'static/js/tesseract-core.wasm.js'


	const worker = new Tesseract.TesseractWorker({
		corePath,
	});

	worker.recognize(file,
		$("#langsel").val()
	)
		// .progress(function (packet) {
		// 	console.info(packet)
		// 	// progressUpdate(packet)

		// })
		.then(function (data) {
			console.log(data)
			console.log("Output through OCR", data.text)
			// console.log()
			document.getElementById('startPre').innerHTML = cleanResult(data.text);
			// progressUpdate({ status: 'done', data: data })
		})
}