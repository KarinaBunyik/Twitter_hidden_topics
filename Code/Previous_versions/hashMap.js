function hashMap(){

	var hashtags = this.username;

	if (hashtags === null){
		return;
	}

	for (var i=0; i<hashtags.length;i++){
		emit(hashtags, {count: 1});
	}


}