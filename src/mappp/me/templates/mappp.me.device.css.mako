<%
fixed_width = min(device.resolution_width, device.max_image_width)
%>
body {
	width: ${fixed_width}px;
}
#header, #footer {
	width: ${int(fixed_width * 0.9)}px;
}
#header img {
    margin-left: -${int(fixed_width * 0.12)}px;
}
ul {
	width: ${int(fixed_width * 0.8 * 0.95)}px;
	margin-left: ${int(fixed_width * 0.8 * 0.05)}px;
}
ul.menu,
#content,
#map,
#map img {
	width: ${int(fixed_width * 0.8)}px;
}
#map img {
    height: ${min(int(fixed_width * 0.8), 200)}px;
}

%if device.pointing_method in ('mouse', 'stylus', 'touchscreen'): #includes desktops
#error,
.button {
	display: block;
	width: 100%;
	height: 4em;
	margin-top: 1em;
    border:1px solid #bce;
    background-color: #cdf;
    text-align: center;
    color: #46d;
    border-radius:1em;
    -webkit-border-radius:1em;
    -moz-border-radius:1em;
}
#error {
    border:1px solid #ecb;
    background-color: #fdc;
    color: #d64;
}
#error:hover,
.button:hover {
	background-color: #bce;
	font-weight: bold;
	text-decoration: none;
}
#error:hover {
	background-color: #ecb;
}
a.button span,
#error span {
	display: block;
	margin: 1em auto;
	font-size: 120%;
    height: 1em;
}
.button.medium {
	display: inline-block;
	width: 8em;
}
.button.small {
	display: inline-block;
	width: 4em;
}
%endif