# 🚀 Inicio Rápido - MongoDB Quiz System

## Paso 1: Navegar al directorio del proyecto

```bash
cd /Users/willdev/github/UNIR/maestria/bd_bigdata/mongodb_quiz_system
```

## Paso 2: Iniciar el servidor

### Opción A: Script automático (Recomendado)

```bash
./start_server.sh
```

### Opción B: Manual

```bash
# 1. Activar ambiente conda
conda activate data

# 2. Iniciar servidor
python app.py
```

## Paso 3: Abrir en el navegador

Abre tu navegador y ve a:

```
http://127.0.0.1:5001
```

o simplemente:

```
http://localhost:5001
```

---

## ⚠️ Solución de Problemas

### Error: "Address already in use" (Puerto 5000)

**Problema resuelto:** La aplicación ahora usa el puerto **5001** en lugar del 5000.

macOS usa el puerto 5000 para AirPlay Receiver. Ya hemos cambiado la aplicación al puerto 5001 para evitar este conflicto.

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solución:**

```bash
conda activate data
pip install flask
```

### La base de datos no existe

**Solución:**

```bash
conda activate data
python init_db.py
```

Esto creará `mongodb_quiz.db` con las 520 preguntas.

### El script start_server.sh no se ejecuta

**Solución:**

```bash
chmod +x start_server.sh
./start_server.sh
```

---

## 📋 Checklist de Inicio

- [ ] Ambiente conda 'data' activado
- [ ] Flask instalado (`pip list | grep -i flask`)
- [ ] Base de datos creada (archivo `mongodb_quiz.db` existe)
- [ ] Puerto 5001 disponible
- [ ] Navegador abierto en http://127.0.0.1:5001

---

## 🎯 Flujo de Uso

1. **Selecciona categorías** (o deja vacío para todas)
2. **Responde 20 preguntas** del examen
3. **Revisa tus resultados** con explicaciones
4. **Consulta tu progreso** en la sección Progress
5. **Revisa tu historial** en la sección History

---

## 🛑 Detener el Servidor

Presiona `Ctrl + C` en la terminal donde está corriendo el servidor.

---

## 📊 Estadísticas del Sistema

- **520 preguntas** totales
- **9 categorías** de MongoDB
- **201 conceptuales** (38.7%)
- **319 de sintaxis** (61.3%)
- **3 niveles:** Fácil, Medio, Difícil

---

## 💡 Consejos

- Usa el **modo de pantalla completa** en el navegador para mejor experiencia
- El sistema guarda automáticamente tu progreso
- Las explicaciones aparecen cuando fallas una pregunta
- Puedes revisar exámenes anteriores en cualquier momento

---

## 📞 Ayuda Adicional

Si tienes problemas, verifica:

1. Que estés en el directorio correcto
2. Que el ambiente conda 'data' esté activado
3. Que Flask esté instalado
4. Que el puerto 5001 no esté en uso
5. Que la base de datos exista

Comando útil para verificar todo:

```bash
conda activate data
python -c "
import sys
print('✅ Python:', sys.version)
import flask
print('✅ Flask:', flask.__version__)
import os
print('✅ BD existe:', os.path.exists('mongodb_quiz.db'))
"
```
