<script>
	import { api } from '$lib/apiMiddleWare.js';

	let audios = [];
	let uploaded_files = [];
	function handleFileUpload(event) {
		const files = event.target.files;
		for (let i = 0; i < files.length; i++) {
			const file = files[i];
			console.log('File:', file);
			console.log('audios:', audios);
			if (uploaded_files.includes(file)) {
				continue;
			}
			uploaded_files.push(file);
			const reader = new FileReader();
			reader.onload = (e) => {
				const audio = e.target.result;
				if (!audios.includes(e.target.result)) {
					audios = [...audios, audio];
				}
			};
			reader.readAsDataURL(file);
		}
	}

	function handleDragOver(event) {
		event.preventDefault();
	}

	function handleDrop(event) {
		event.preventDefault();
		const files = event.dataTransfer.files;
		for (let i = 0; i < files.length; i++) {
			const file = files[i];
			const reader = new FileReader();
			if (uploaded_files.includes(file)) {
				continue;
			}
			uploaded_files.push(file);
			reader.onload = (e) => {
				const audio = e.target.result;
				if (!audios.includes(e.target.result)) {
					audios = [...audios, audio];
				}
			};
			reader.readAsDataURL(file);
		}
	}

	async function handleSubmit(event) {
		event.preventDefault();
		const formData = new FormData(event.target);
		const files = formData.getAll('audios');
		console.log('Files:', files);

		for (const file of files) {
			formData.append('files', file);
		}

		try {
			const response = await api.post('/user/upload', formData, {
				headers: {
					'Content-Type': 'multipart/form-data'
				}
			});
			if (response.status != 200) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const responseData = await response.data;
			console.log('Response:', responseData);
		} catch (error) {
			console.error('Error:', error);
		}
	}
</script>

<div
	class="upload-container"
	on:dragover={handleDragOver}
	on:drop={handleDrop}
	role="button"
	tabindex="0"
>
	<p>Drag and drop your files here</p>
	<br>
	<form on:submit={handleSubmit} style="display:flex; flex-direction:column; justify-content: center; align-items:center">
		<input type="file" id ="audios" name="audios" class="hidden" multiple accept="audio/*" on:change={handleFileUpload} />
		
		<button type="button" class="btn variant-filled"><label for="audios">Select Custom Audio Files</label></button>
		<br />

		<div class="uploaded-audios">
			{#each audios as audio, i}
				<div class="uploaded-audio">
					<audio controls>
						<source src={audio} type="audio/mpeg">
						Your browser does not support the audio element.
					</audio>
					<p id="filename">{uploaded_files[i].name}</p>
				</div>
			{/each}
		</div>
		
		<input type="submit" value="Upload" class="upload-button" />
	</form>
</div>

<style lang="postcss">
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
	.upload-button {
		margin-top: 10px;
		padding: 10px 20px;
		border: none;
		border-radius: 5px;
		background-color: #333333;
		color: #ffffff;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}
</style>
