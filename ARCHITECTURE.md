# Arquitectura del Proyecto Chatbot Académico

## 🏗️ Estructura Mejorada

### Frontend (React + Vite)

#### 📁 `src/components/`
- **`Chat/`**: Componentes específicos del chat
  - `ChatContainer.jsx`: Contenedor principal del chat
  - `MessageList.jsx`: Lista de mensajes con animaciones
  - `MessageInput.jsx`: Campo de entrada de mensajes
  - `QuickActions.jsx`: Botones de preguntas rápidas
  - `ChatFooter.jsx`: Pie del chat con acciones
- **`Admin/`**: Componentes de administración (futuro)
- **`common/`**: Componentes reutilizables
  - `Header.jsx`: Barra de navegación con tema

#### 📁 `src/hooks/`
- **`useChat.js`**: Lógica del chat (mensajes, envío, limpieza)
- **`useTheme.js`**: Gestión del tema (dark/light mode)

#### 📁 `src/services/`
- **`api.js`**: Servicio de comunicación con el backend

#### 📁 `src/utils/`
- **`constants.js`**: Constantes de la aplicación

#### 📁 `src/styles/`
- Estilos adicionales (futuro)

### Backend (Flask)

#### 📁 `backend/`
- **`app.py`**: Aplicación principal Flask
- **`models.py`**: Modelos de base de datos
- **`config.py`**: Configuración
- **`database/`**: Servicios de base de datos
- **`services/`**: Lógica de negocio
- **`utils/`**: Utilidades de procesamiento
- **`routes/`**: Endpoints de API

### Tests

#### 📁 `tests/`
- **`unit/`**: Tests unitarios
- **`integration/`**: Tests de integración
- **`e2e/`**: Tests end-to-end

## 🔄 Flujo de Datos

```
Usuario → MessageInput → useChat → apiService → Backend
                ↓
            MessageList ← useChat ← apiService ← Backend
```

## 🎨 Patrones de Diseño

### 1. **Separación de Responsabilidades**
- **Componentes**: Solo UI y eventos
- **Hooks**: Lógica de estado y efectos
- **Servicios**: Comunicación externa
- **Utils**: Constantes y utilidades

### 2. **Composición de Componentes**
- Componentes pequeños y reutilizables
- Props bien definidas
- Lógica encapsulada en hooks

### 3. **Gestión de Estado**
- Estado local en componentes
- Estado compartido en hooks
- Configuración en constantes

## 🚀 Beneficios de la Nueva Estructura

### ✅ **Mantenibilidad**
- Código más fácil de entender y modificar
- Componentes con responsabilidades claras
- Separación lógica de funcionalidades

### ✅ **Escalabilidad**
- Fácil agregar nuevos componentes
- Estructura preparada para crecimiento
- Patrones consistentes

### ✅ **Reutilización**
- Componentes modulares
- Hooks reutilizables
- Constantes centralizadas

### ✅ **Testing**
- Componentes aislados fáciles de testear
- Hooks independientes
- Estructura de tests organizada

## 🔧 Configuración

### Variables de Entorno
- `env.example`: Plantilla de configuración
- Configuración separada para frontend y backend
- Fácil despliegue en diferentes entornos

### Scripts de Automatización
- `start.sh`: Inicio automático de servicios
- `stop.sh`: Parada limpia de servicios
- Verificaciones de dependencias

## 📈 Métricas de Mejora

| Aspecto | Antes | Después |
|---------|-------|---------|
| Líneas por archivo | ~316 (App.jsx) | ~42 (App.jsx) |
| Componentes | 1 monolítico | 6 modulares |
| Reutilización | Baja | Alta |
| Testing | Difícil | Fácil |
| Mantenimiento | Complejo | Simple |

## 🎯 Próximos Pasos

1. **Implementar tests** para cada componente
2. **Agregar componentes de Admin** para gestión
3. **Optimizar rendimiento** con React.memo
4. **Implementar PWA** para funcionalidad offline
5. **Agregar internacionalización** (i18n) 