<template>
  <main class="container">
    <h1>IoT Dashboard</h1>
    <p>{{ message }}</p>
    <button @click="fetchMessage">Fetch latest message</button>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const message = ref('Loading message from backend...')

async function fetchMessage() {
  try {
    const response = await axios.get('/api/message')
    message.value = response.data.message
  } catch (error) {
    message.value = 'Unable to reach the backend API.'
    console.error(error)
  }
}

onMounted(fetchMessage)
</script>

<style scoped>
.container {
  margin: 0 auto;
  padding: 2rem;
  max-width: 640px;
  font-family: system-ui, sans-serif;
  text-align: center;
}

button {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 999px;
  background: #1f2937;
  color: #fff;
  cursor: pointer;
}

button:hover {
  background: #111827;
}
</style>
