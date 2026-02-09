<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Сообщения Avito</h2>
    <div class="bg-white rounded shadow overflow-hidden">
      <table class="w-full text-left">
        <thead class="bg-gray-50"><tr><th class="p-3">ID</th><th class="p-3">Чат</th><th class="p-3">Отправитель</th><th class="p-3">Текст</th><th class="p-3">Направление</th><th class="p-3">Автоответ</th></tr></thead>
        <tbody>
          <tr v-for="m in store.messages" :key="m.id" class="border-t">
            <td class="p-3">{{ m.id }}</td><td class="p-3">{{ m.chat_id }}</td><td class="p-3">{{ m.sender_name || '—' }}</td>
            <td class="p-3 max-w-xs truncate">{{ m.message_text }}</td>
            <td class="p-3"><span :class="m.direction === 'incoming' ? 'text-blue-600' : 'text-green-600'">{{ m.direction === 'incoming' ? 'Входящее' : 'Исходящее' }}</span></td>
            <td class="p-3">{{ m.is_auto_replied ? 'Да' : '—' }}</td>
          </tr>
          <tr v-if="!store.messages.length"><td colspan="6" class="p-3 text-gray-500 text-center">Нет сообщений</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAvitoStore } from '../../store'
const store = useAvitoStore()
onMounted(() => store.fetchMessages())
</script>
