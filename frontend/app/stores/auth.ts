export const useAuthStore = defineStore('auth', () => {
  const access = ref(''); const refresh = ref(''); const user = ref<any>(null)
  const api = useRuntimeConfig().public.apiBase
  async function login(email:string,password:string){ const data:any=await $fetch(`${api}/auth/login`,{method:'POST',body:{email,password}}); access.value=data.access; refresh.value=data.refresh; await loadUser() }
  async function loadUser(){ user.value=await $fetch(`${api}/users/me`,{headers:{Authorization:`Bearer ${access.value}`}}) }
  function logout(){ access.value=''; refresh.value=''; user.value=null; navigateTo('/login') }
  return {access,refresh,user,login,loadUser,logout}
})
