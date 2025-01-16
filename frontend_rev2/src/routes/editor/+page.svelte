<svelte:head>
	<link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
</svelte:head>
<script>
	import { AppShell, AppBar, popup } from '@skeletonlabs/skeleton';
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	import { getDecoded, api } from '../../lib/apiMiddleWare';
import pkg from 'plyr';
const Plyr  = pkg;

	const STARTTRANSITIONS = [{key: 'none', name: "None" }, {key: 'crossfadein', name: "FadeIn" }, {key: 'slidein', name: "SlideIn" }];
	const ENDTRANSITIONS = [{key: 'none', name: "None" }, {key: 'crossfadeout', name: "FadeOut" }, {key: 'slideout', name: "SlideOut" }];
	let seconds = 300;

	let scale = 100;

	let images = [];
	// {objecturi: , path: }

	let audios = [];


	function actualFileName(path){
		return path.split('.').slice(1).join('.');
	}



	let timelineimages = [];
	let imgclips = [];
	let audioclips = [];
	// startTransition, duration, endTransition, path
	// transition must also have duration
	function addtoTimeline(image) {
		console.log(image);
		return (event) => {
			timelineimages = [...timelineimages, image];
			imgclips.push({duration: 1, startTransition: {
				type: 'none',
				duration: 0
			}, endTransition: {
				type: 'none',
				duration: 0
			},
			path: image.path
		});
		};
	}
	function addAudToTimeline(audio) {
		return (event) => {
			timelineimages = [...timelineimages, image];
			imgclips.push({duration: 1, startTransition: {
				type: 'none',
				duration: 0
			}, endTransition: {
				type: 'none',
				duration: 0
			},
			path: image.path
		});
		};
	}

	let popupSettings = [];

	$: {
		popupSettings = timelineimages.map((image, index) => ({
			event: 'click',
			target: 'popupClick-' + index,
			placement: 'top'
		}));
	}

	function isImage(media) {
		return media.mediatype == 'image';
	}

	function isAudio(media) {
		return media.mediatype == 'audio';
	}
	let player;
	onMount(async () => {
		
	 player = new Plyr('#player', {
		controls: ['rewind','play','fast-forward', 'progress', 'current-time', 'mute', 'volume', 'settings','fullscreen' ],
		settings: ['quality','speed'],
		i18n: {
		'fastForward': 'Forward 3 secs',
		'rewind': 'Rewind 3 secs',
		},

		blankVideo: 'https://cdn.plyr.io/static/blank.mp4',
	});
	player.source = {
		type: 'video',
		title: 'Rendered Video',
		sources: [{
			src: '',
			type: 'video/mp4'
		}]
	}
		console.log(getDecoded());
		let medias = (await api.get('/preloadedaudio')).data.map((audio) => ({
			mediatype: 'audio',
			filename: audio
		})).concat(getDecoded().paths);
		// let medias = getDecoded().paths;
		console.log(medias);
		let tasks = [];
		let t = 0;
		async function mediadd() {
			if (t >= medias.length) {
				return;
			}
			let media = medias[t];
			let i = (
					await api.get(`/getfile/${media.filename}`, {
						responseType: 'blob'
					})
				).data;
				console.log(i);
				var uri = URL.createObjectURL(i);
			if (isImage(media)) {
				images = [...images, {objecturi: uri, path: media.filename}];
			} else if(isAudio(media)){
				console.log(uri);
				audios = [...audios, {objecturi: uri, path: media.filename}];
			}
			t++;
			// this is to ensure that requests are sent linearly and not all at once
			mediadd();
		}
		mediadd();
	});


	const renderer = async ()=>{
		let file = await api.post('/edit', {images: imgclips, audios: audioclips}, {
			responseType: 'blob'
		});
		console.log(file);
		
		player.source = {
			type: 'video',
			title: 'Rendered Video',
			sources: [{
				src: URL.createObjectURL(file.data),
				type: 'video/mp4'
			}]
		}
	}

let searchText = '';
</script>

<!-- svelte-ignore a11y-img-redundant-alt -->
<AppShell regionPage="relative" slotfooter="sticky top-100 z-10">
	<svelte:fragment slot="sidebarLeft">
		<div class="images_nav">
			<div class="nava">
	</div>
			<div class="navb">
				<div id="shell-title" class="m-1">Uploaded-Images</div>

				<br />
				<input
					id="searchbox"
					class="input m-2"
					title="Input (text)"
					type="text"
					placeholder="Search for an image by filename"
					bind:value={searchText}
				/>
				<br />
				<div class="uploaded-images">
					{#each images as image}
					{#if actualFileName(image.path).includes(searchText)}
						<button on:click={addtoTimeline(image)}>
							<img class="uploaded-image" src={image.objecturi} alt="hi"  />
							{actualFileName(image.path)}
						</button>
						{/if}
					{/each}
				</div>
			</div>
		</div>
	</svelte:fragment>

	<svelte:fragment slot="sidebarRight">
		<div class="navc">
			<div class="uploaded-audios">
				{#each audios as audio}
					<div class="uploaded-audio">
						<audio src={audio.objecturi} controls></audio>
						{actualFileName(audio.path)}
					</div>
				{/each}
			</div>
		</div>
	</svelte:fragment>

	 <div class="mediaplayer">
		<!-- svelte-ignore a11y-media-has-caption -->
		<video id="player" playsinline controls rewind>
			<source src="" type="video/mp4" />
		  
		  </video>
		<!-- <video-js
		id="my-video"
		class="video-js"
		controls
		preload="auto"
		width="640"
		height="264"
		poster="MY_VIDEO_POSTER.jpg"
	  >	
		<source src="https://vjs.zencdn.net/v/oceans.mp4" type="video/mp4" />
		<p class="vjs-no-js">
		  To view this video please enable JavaScript, and consider upgrading to a
		  web browser that
		  <a href="https://videojs.com/html5-video-support/" target="_blank"
			>supports HTML5 video</a
		  >
		</p>
	  </video-js> -->
	</div> 

	<svelte:fragment slot="pageFooter">
		<div class="navb">
			<div class="media-controls">
				<div style="padding-top:0.2vw; 	padding-right: 20vw;padding-left: 20vw;"><button class="input" style="padding: 0.5vw" on:click={renderer} >Render</button></div></div>
			<div
				class="timeline snap-x scroll-px-4 snap-mandatory scroll-smooth flex gap-0 overflow-x-auto px-4 py-10"
			>
				<div class="timeline-bg-wrapper">
					<svg height="20" width={seconds * scale} class="timeline_bg">
						{#each Array(seconds) as marker, i}
							<rect x={scale * i} y="0" width="2" height="200" />
						{/each}

						{#each Array(seconds) as marker, i}
							{#if i % 5 === 0}
								<text x={scale * i + 5} y="15">{i}s</text>
							{/if}
						{/each}
					</svg>
					<div class="timeline-images-container">
						{#each timelineimages as timelineimage, i}
							<div class="timeline-image-wrapper">
								<img
									width="{imgclips[i].duration*scale + 'px'};"
									id={'image-' + i}
									class="timeline-image"
									src={timelineimage.objecturi}
									alt="hi"
									use:popup={popupSettings[i]}
								/>
								<div class="card p-4 gap-4 variant-filled-secondary" data-popup={'popupClick-' + i}>
									<form id={'image-duration-' + i} >
										<label for={'duration' + i}>Duration (in seconds):</label>
										<input
											class="input"
											type="number"
											step="0.5"
											name="duration"
											bind:value={imgclips[i].duration}
										/>
										<table>
											<tr>
												<th>
													Start Transition
												</th>
												<th>
													End Transition
												</th>
											</tr>
											<tr>
												<td>
												<select
												name="startTransition"
												id={'startTransition' + i}
												class="input"
												bind:value={imgclips[i].startTransition.type}
												>
												{#each STARTTRANSITIONS as transition}
													<option value={transition.key}>{transition.name}</option>
												{/each}
											</select>
											</td>
											<td>
												<select
												name="endTransition"
												id={'endTransition' + i}
												class="input"
												bind:value={imgclips[i].endTransition.type}
												>
												{#each ENDTRANSITIONS as transition}
													<option value={transition.key}>{transition.name}</option>
												{/each}
											</select>
											</td>
											</tr>
											<tr>
												<td>
													<!-- Duration for transition -->
													Duration: <input class="input" type="number" name="startduration" bind:value={imgclips[i].startTransition.duration} />
												</td>
												<td>
													<!-- Duration for transition -->
													Duration: <input class="input" type="number" name="endduration" bind:value={imgclips[i].endTransition.duration} />
												</td>
											</tr>
										</table>
										<input type="hidden" name="imageIndex" value={i} />
									</form>

									<div class="arrow variant-filled-primary" />
								</div>
							</div>
						{/each}
					</div>
				</div>
			</div>
		</div>
	</svelte:fragment>
</AppShell>

<style lang="postcss">
	.images_nav {
		height: 80vh;
	}
	.nava {
		background-color: #202941;
		width: 100%;
		margin-bottom: 5px;
		padding: 5px;
		box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
		overflow: hidden;
	}
	.navb {
		z-index: 10;
		background-color: #202941;
		width: 100%;
		padding: 5px;
		box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
	}
	.navc{
		height: 100%;
		background-color: #202941;
	}
	.image-uploader {
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		margin-top: 10px;
		padding: 20px;
	}
	.image-uploader img {
		display: inline-block;
	}
	.uploaded-images {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		justify-content: center;
		margin-top: 20px;
		overflow-y: scroll;
		scroll-behavior: smooth;
	}
	.uploaded-image {
		height: 100px;
		width: 100px;
		margin: 10px;
		object-fit: contain;
	}

	.timeline {
		height: 200px;
	}

	.timeline-image {
		height: 100px;
		object-fit: cover;
	}

	.timeline_bg {
		background: #ccc;
	}

	.timeline-bg-wrapper {
		width: 100%;
	}

	.timeline-images-container {
		width: 100%;
		display: flex;
		flex-wrap: nowrap; /* Ensures images stay in a single line */
	}

	.timeline-image-wrapper {
		flex: 0 0 auto;
		max-width: none;
		width: auto;
	}

	form .input {
		margin-top: 10px;
		margin-bottom: 10px;
	}

	form button {
		margin-bottom: 10px;
	}

	.upload-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center	;
		margin-top: 100px;
		margin-left: 10%;
		margin-right: 10%;
		border: 2px dashed #ccc;
		padding: 20px;
		padding-top: 30px;
	}

	.uploaded-audios {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		margin-top: 20px;
	}

	.uploaded-audio {
		margin: 10px;
		object-fit: cover;
	}
	#filename{
		max-width: 300px;
		text-overflow: ellipsis;
	}
</style>
