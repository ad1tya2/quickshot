<!-- YOU CAN DELETE EVERYTHING IN THIS PAGE -->
<script>
	import axios from 'axios';
	import { writable } from 'svelte/store'
	import { onMount } from 'svelte'
	import { getDecoded } from '../../../lib/apiMiddleWare';


	let username = ''; //intit glbal
	let password = '';

	async function hash(string) {
		const utf8 = new TextEncoder().encode(string);
		const hashBuffer = await crypto.subtle.digest('SHA-256', utf8);
		const hashArray = Array.from(new Uint8Array(hashBuffer));
		const hashHex = hashArray.map((bytes) => bytes.toString(16).padStart(2, '0')).join('');
		return hashHex;
	}

	async function login() {
		try {
			const response = await axios.get('http://api.mossdaddy.tech/login', {
				params: {
					username: username,
					password: await hash(password)
				}
			});

			if (response.data.jwt) {
				localStorage.setItem('jwt', response.data.jwt);
				if(getDecoded(response.data.jwt).isadmin) window.location.href='/admin'
				else
				window.location.href='/user/dashboard'
			} else {
				console.error(response.data.message);
			}
		} catch (error) {
			if (
				error.response &&
				error.response.status === 401 &&
				error.response.data.message === 'Invalid credentials'
			) {
				alert(error.response.data.message);
			}
		}admin	
	}
	onMount(async () => {
		if (typeof localStorage !== 'undefined') {
            const storedJWT = localStorage.getItem('jwt');
            if (storedJWT) {
				
				if(getDecoded(storedJWT).isadmin) window.location.href='/admin'
				else
				window.location.href = '/user/dashboard';
            }
        }
    });
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Login</h2>
		<form on:submit|preventDefault={login} class="login-form">
			<label class="label">
				<span>Username</span>
				<br />
				<input bind:value={username} class="input variant-form-material" type="text" placeholder="Username" />
			</label>
			<br />
			<label class="label">
				<span>Password</span>
				<br />
				<input bind:value={password} class="input variant-form-material" type="password" placeholder="Password" />
			</label>
			<br />
			<button type="submit" class="btn variant-filled">Login</button>
			<br />
		</form>
		<a href="/register" class="text-primary-400">Don't have an account? Register</a> 
	</div>
</div>

<style lang="postcss">
	.login-form {
		background-color: #2c3656;
		border-radius: 25px;
		width: 30vw;
		padding: 30px;
		height: 32vh;
	}
</style>
