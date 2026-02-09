<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Шаблоны объявлений</h2>
    <div class="bg-white rounded shadow overflow-hidden">
      <table class="w-full text-left">
        <thead class="bg-gray-50"><tr><th class="p-3">ID</th><th class="p-3">Название</th><th class="p-3">Категория</th><th class="p-3">Заголовок</th></tr></thead>
        <tbody>
          <tr v-for="t in store.templates" :key="t.id" class="border-t">
            <td class="p-3">{{ t.id }}</td><td class="p-3">{{ t.name }}</td><td class="p-3">{{ t.category || '—' }}</td><td class="p-3">{{ t.title }}</td>
          </tr>
          <tr v-if="!store.templates.length"><td colspan="4" class="p-3 text-gray-500 text-center">Нет шаблонов</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAvitoStore } from '../../store'
const store = useAvitoStore()
onMounted(() => store.fetchTemplates())
</script>
