function findScore(score) {

	score = 0;
	const form = document.querySelector("form");

	const data = new FormData(form);
	let answers = data.values();
	var stuff = data.entries();

	answers = ["", "c", "d", "c", "a"]
	let counter = 0;

	for (var pair of stuff) {
		if(String(pair[1]) == answers[counter]){
			score++;
		}
		// console.log(pair[0]+ ', ' + pair[1] + ", " + answers[counter]); 
		counter++;
	}	
	// console.log(score);
	output.innerHTML = `Score: ${score}/4` ;
}