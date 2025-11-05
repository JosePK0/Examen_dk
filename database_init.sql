-- ============================================
-- Script de inicialización de base de datos
-- HelpDeskPro - Sistema de Gestión de Tickets
-- ============================================

-- Crear base de datos (si no existe)
CREATE DATABASE IF NOT EXISTS helpdeskpro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE helpdeskpro;

-- ===========================
-- 1️⃣ Tabla: usuarios
-- ===========================
CREATE TABLE IF NOT EXISTS usuarios (
    IDusuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('usuario', 'tecnico', 'admin') DEFAULT 'usuario',
    activo TINYINT(1) DEFAULT 1,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ===========================
-- 2️⃣ Tabla: tickets
-- ===========================
CREATE TABLE IF NOT EXISTS tickets (
    IDticket INT AUTO_INCREMENT PRIMARY KEY,
    usuarioID INT NOT NULL,
    tecnicoID INT DEFAULT NULL,
    descripcion TEXT NOT NULL,
    prioridad ENUM('baja', 'media', 'alta', 'critica') DEFAULT 'media',
    estado ENUM('abierto', 'en_proceso', 'cerrado') DEFAULT 'abierto',
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_ticket_usuario FOREIGN KEY (usuarioID) REFERENCES usuarios(IDusuario)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ticket_tecnico FOREIGN KEY (tecnicoID) REFERENCES usuarios(IDusuario)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ===========================
-- 3️⃣ Datos de ejemplo (opcional)
-- ===========================

-- Insertar usuarios de ejemplo
INSERT INTO usuarios (nombre, correo, contrasena, rol, activo) VALUES
('Juan Pérez', 'juan.perez@empresa.com', 'password123', 'usuario', 1),
('María García', 'maria.garcia@empresa.com', 'password123', 'usuario', 1),
('Carlos López', 'carlos.lopez@empresa.com', 'password123', 'tecnico', 1),
('Ana Martínez', 'ana.martinez@empresa.com', 'password123', 'tecnico', 1),
('Admin Sistema', 'admin@empresa.com', 'admin123', 'admin', 1);

-- Insertar tickets de ejemplo
INSERT INTO tickets (usuarioID, tecnicoID, descripcion, prioridad, estado) VALUES
(1, 3, 'No puedo acceder a mi correo electrónico', 'alta', 'abierto'),
(2, NULL, 'Mi impresora no funciona correctamente', 'media', 'abierto'),
(1, 4, 'El sistema está muy lento', 'critica', 'en_proceso');

