<script>
    import {onMount} from 'svelte';
    import { getDecoded, api } from '../../lib/apiMiddleWare';
    let users = [];
    onMount(async () => {
        const res = ( await api.get('/users')).data
        if(!res){
        alert("Unauthorized");
         window.location.href = "/login";
        }else{
            users = res;   
         }
 
 
    });
 </script>
 <body>
     <div class="table-container">
         <table class="table table-hover">
             <thead>
                 <tr>
                     <th class="border-r-2">Username</th>
                     <th class="border-r-2">Email</th>
                     <th>User Type</th>
                 </tr>
             </thead>
             <tbody>
                 {#each users as user}
                     <tr>
                         <td class="border-r-2">{user.username}</td>
                         <td class="border-r-2">{user.email}</td>
                         <td>{user.isadmin?"Admin":"User"}</td>
                     </tr>
                 {/each}
             </tbody>
         </table>
     </div>
 </body>
 
 <style>
 .table-container{
     display: grid;
     width: 80vw;
     margin: 20px;
     padding: 20px;
 }
 </style>