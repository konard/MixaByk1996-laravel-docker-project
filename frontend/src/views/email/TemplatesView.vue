<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Шаблоны писем</h2>
      <button @click="showForm = !showForm" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        {{ showForm ? 'Отмена' : '+ Создать' }}
      </button>
    </div>

    <form v-if="showForm" @submit.prevent="add" class="bg-white p-4 rounded shadow mb-6 space-y-3">
      <input v-model="form.name" placeholder="Название шаблона" class="w-full border rounded p-2" required />
      <input v-model="form.subject" placeholder="Тема письма" class="w-full border rounded p-2" required />
      <textarea v-model="form.html_content" placeholder="HTML содержимое (поддерживает {имя}, {город}, {последние_закупки})" class="w-full border rounded p-2" rows="6" required></textarea>
      <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">Создать</button>
    </form>

    <div class="bg-white rounded shadow overflow-hidden">
      <table class="w-full text-left">
        <thead class="bg-gray-50"><tr><th class="p-3">ID</th><th class="p-3">Название</th><th class="p-3">Тема</th><th class="p-3">Создан</th></tr></thead>
        <tbody>
          <tr v-for="t in store.templates" :key="t.id" class="border-t">
            <td class="p-3">{{ t.id }}</td><td class="p-3">{{ t.name }}</td><td class="p-3">{{ t.subject }}</td><td class="p-3">{{ t.created_at?.slice(0, 10) || '—' }}</td>
          </tr>
          <tr v-if="!store.templates.length"><td colspan="4" class="p-3 text-gray-500 text-center">Нет шаблонов</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useEmailStore } from '../../store'
const store = useEmailStore()
const showForm = ref(false)
const form = ref({ name: '', subject: '', html_content: '' })
const add = async () => { await store.createTemplate(form.value); form.value = { name: '', subject: '', html_content: '' }; showForm.value = false }
onMounted(() => store.fetchTemplates())
</script>
