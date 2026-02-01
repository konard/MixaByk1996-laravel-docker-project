<template>
  <div class="min-h-screen flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-800 text-white flex-shrink-0">
      <div class="p-4">
        <h1 class="text-xl font-bold">Avito Bot</h1>
        <p class="text-gray-400 text-sm">Панель управления</p>
      </div>
      <nav class="mt-4">
        <router-link to="/" class="sidebar-link" active-class="bg-gray-700">
          📊 Дашборд
        </router-link>
        <div class="px-4 pt-4 pb-1 text-xs text-gray-500 uppercase">Avito</div>
        <router-link to="/avito/accounts" class="sidebar-link" active-class="bg-gray-700">
          👤 Аккаунты
        </router-link>
        <router-link to="/avito/ads" class="sidebar-link" active-class="bg-gray-700">
          📋 Объявления
        </router-link>
        <router-link to="/avito/templates" class="sidebar-link" active-class="bg-gray-700">
          📝 Шаблоны
        </router-link>
        <router-link to="/avito/competitors" class="sidebar-link" active-class="bg-gray-700">
          🔍 Конкуренты
        </router-link>
        <router-link to="/avito/messages" class="sidebar-link" active-class="bg-gray-700">
          💬 Сообщения
        </router-link>
        <div class="px-4 pt-4 pb-1 text-xs text-gray-500 uppercase">Email</div>
        <router-link to="/email/campaigns" class="sidebar-link" active-class="bg-gray-700">
          📧 Кампании
        </router-link>
        <router-link to="/email/templates" class="sidebar-link" active-class="bg-gray-700">
          📄 Шаблоны
        </router-link>
        <div class="px-4 pt-4 pb-1 text-xs text-gray-500 uppercase">CRM</div>
        <router-link to="/contacts" class="sidebar-link" active-class="bg-gray-700">
          👥 Контакты
        </router-link>
        <router-link to="/contacts/segments" class="sidebar-link" active-class="bg-gray-700">
          🏷 Сегменты
        </router-link>
      </nav>
    </aside>

    <!-- Main content -->
    <main class="flex-1 p-6">
      <router-view />
    </main>
  </div>
</template>

<style>
.sidebar-link {
  @apply block px-4 py-2 text-sm hover:bg-gray-700 transition-colors;
}
</style>
