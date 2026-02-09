<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Сегменты контактов</h2>
      <button @click="showForm = !showForm" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        {{ showForm ? 'Отмена' : '+ Создать' }}
      </button>
    </div>

    <form v-if="showForm" @submit.prevent="add" class="bg-white p-4 rounded shadow mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
      <input v-model="form.name" placeholder="Название сегмента" class="border rounded p-2" required />
      <input v-model="form.description" placeholder="Описание" class="border rounded p-2" />
      <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">Создать</button>
    </form>

    <div class="bg-white rounded shadow overflow-hidden">
      <table class="w-full text-left">
        <thead class="bg-gray-50"><tr><th class="p-3">ID</th><th class="p-3">Название</th><th class="p-3">Описание</th><th class="p-3">Тип</th></tr></thead>
        <tbody>
          <tr v-for="s in store.segments" :key="s.id" class="border-t">
            <td class="p-3">{{ s.id }}</td><td class="p-3">{{ s.name }}</td><td class="p-3">{{ s.description || '—' }}</td>
            <td class="p-3">{{ s.is_dynamic ? 'Динамический' : 'Статический' }}</td>
          </tr>
          <tr v-if="!store.segments.length"><td colspan="4" class="p-3 text-gray-500 text-center">Нет сегментов</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useContactStore } from '../../store'
const store = useContactStore()
const showForm = ref(false)
const form = ref({ name: '', description: '' })
const add = async () => { await store.createSegment(form.value); form.value = { name: '', description: '' }; showForm.value = false }
onMounted(() => store.fetchSegments())
</script>
