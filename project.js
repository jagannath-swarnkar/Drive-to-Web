const express = require('express');
const app = express();

app.get('/photos',(req,res)=>{
	res.sendFile(__dirname + '/project.html')
});

app.listen(8080);