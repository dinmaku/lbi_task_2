<template>
  <div class="landing">
    <h1>Welcome, {{ userEmail }}!</h1>
    <p>You have successfully logged in.</p>
    <button @click="logout">Logout</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// For demo, hardcoding a user email
const userEmail = ref('testuser@example.com')

const router = useRouter()

function logout() {
  // Here you would clear auth tokens, user state, etc.
  // Then redirect to login page
  router.push('/')
}
</script>

<style scoped>
.landing {
  max-width: 400px;
  margin: 50px auto;
  text-align: center;
  font-family: Arial, sans-serif;
}
button {
  margin-top: 20px;
  padding: 10px 20px;
  cursor: pointer;
}
</style>