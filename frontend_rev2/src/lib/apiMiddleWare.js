import axios from 'axios';
import { jwtDecode } from "jwt-decode";
let api;

api = axios.create({
  baseURL: 'http://api.mossdaddy.tech',
  timeout: 10000
});


api.interceptors.request.use(
  function (config)  {
    const jwt = localStorage.getItem('jwt');
    if (jwt) {
      config.headers['jwt'] = jwt;
    }   
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    if(response.data ) {
      if(response.data.jwt){
    localStorage.setItem('jwt', response.data.jwt);
    console.log(response.data.jwt);
    }
    if(response.data.message)
    {
      alert(response.data.message);
    }
  }
  return response;
},
  (error) => {
    if(error.response && error.response.status === 401) {
      localStorage.removeItem('jwt'); 
        window.location.href = '/'; 
    } else {
      console.log(error);
    }
    return "";
  }
);

const getDecoded = ()=>{
  return jwtDecode(localStorage.getItem('jwt'));
}


export { api,getDecoded };
