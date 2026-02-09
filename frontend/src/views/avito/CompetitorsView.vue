<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Мониторинг конкурентов</h2>
      <button @click="showForm = !showForm" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        {{ showForm ? 'Отмена' : '+ Добавить' }}
      </button>
    </div>

    <form v-if="showForm" @submit.prevent="add" class="bg-white p-4 rounded shadow mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
      <input v-model="form.name" placeholder="Название" class="border rounded p-2" required />
      <input v-model="form.search_query" placeholder="Поисковый запрос" class="border rounded p-2" required />
      <input v-model="form.region" placeholder="Регион" class="border rounded p-2" />
      <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">Добавить</button>
    </form>

    <div class="bg-white rounded shadow overflow-hidden">
      <table class="w-full text-left">
        <thead class="bg-gray-50"><tr><th class="p-3">ID</th><th class="p-3">Название</th><th class="p-3">Запрос</th><th class="p-3">Регион</th><th class="p-3">Статус</th></tr></thead>
        <tbody>
          <tr v-for="c in store.competitors" :key="c.id" class="border-t">
            <td class="p-3">{{ c.id }}</td><td class="p-3">{{ c.name }}</td><td class="p-3">{{ c.search_query }}</td>
            <td class="p-3">{{ c.region || '—' }}</td>
            <td class="p-3"><span :class="c.is_active ? 'text-green-600' : 'text-gray-500'">{{ c.is_active ? 'Активен' : 'Остановлен' }}</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAvitoStore } from '../../store'
const store = useAvitoStore()
const showForm = ref(false)
const form = ref({ name: '', search_query: '', region: '' })
const add = async () => { await store.createCompetitor(form.value); form.value = { name: '', search_query: '', region: '' }; showForm.value = false }
onMounted(() => store.fetchCompetitors())
</script>
