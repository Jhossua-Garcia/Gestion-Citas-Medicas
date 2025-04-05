create database Citas_Medicas_T03

use Citas_Medicas_T03


CREATE TABLE Pacientes (
    id_paciente INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100),
    edad INT,
    telefono NVARCHAR(20),
    direccion VARCHAR(255) NOT NULL
);

INSERT INTO Pacientes (nombre, edad, telefono, direccion) VALUES
('Juan Pérez', 30, '87654321', 'Calle 1'),
('María Gómez', 25, '12345678', 'Avenida 2');

CREATE TABLE Doctores (
    id_doctor INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100),
    especialidad VARCHAR(100),
    telefono NVARCHAR(20)
);

INSERT INTO Doctores (nombre, especialidad, telefono) VALUES
('Dr. Rodríguez', 'Cardiología', '22224321'),
('Dra. Fernández', 'Dermatología', '1118765');

CREATE TABLE Citas (
    id_cita INT IDENTITY(1,1) PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_doctor INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    estado VARCHAR(20) CHECK (estado IN ('Pendiente', 'Confirmada', 'Cancelada')) NOT NULL,
    CONSTRAINT FK_Citas_Paciente FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente),
    CONSTRAINT FK_Citas_Doctor FOREIGN KEY (id_doctor) REFERENCES Doctores(id_doctor)
);

INSERT INTO Citas (id_paciente, id_doctor, fecha_hora, estado) VALUES
(1, 1, '2025-04-10 10:00:00', 'Pendiente'),
(2, 2, '2025-04-11 11:30:00', 'Confirmada');

CREATE TABLE Especialidades (
    id_especialidad INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);


CREATE TABLE Doctores_Especialidades (
    id_doctor INT NOT NULL,
    id_especialidad INT NOT NULL,
    PRIMARY KEY (id_doctor, id_especialidad),
    CONSTRAINT FK_DocEsp_Doctor FOREIGN KEY (id_doctor) REFERENCES Doctores(id_doctor),
    CONSTRAINT FK_DocEsp_Especialidad FOREIGN KEY (id_especialidad) REFERENCES Especialidades(id_especialidad)
);


CREATE TABLE Historial_Citas (
    id_historial INT IDENTITY(1,1) PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_doctor INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    diagnostico TEXT NULL,
    CONSTRAINT FK_Historial_Paciente FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente),
    CONSTRAINT FK_Historial_Doctor FOREIGN KEY (id_doctor) REFERENCES Doctores(id_doctor)
);

-- Tabla de Historial de Pacientes
CREATE TABLE Historial_Pacientes (
    id_historial_paciente INT IDENTITY(1,1) PRIMARY KEY,
    id_paciente INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    diagnostico TEXT NULL,
    tratamiento TEXT NULL,
    CONSTRAINT FK_HistorialPacientes_Paciente FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente)
);

-- Tabla de Historial de Doctores
CREATE TABLE Historial_Doctores (
    id_historial_doctor INT IDENTITY(1,1) PRIMARY KEY,
    id_doctor INT NOT NULL,
    id_paciente INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    observaciones TEXT NULL,
    CONSTRAINT FK_HistorialDoctores_Doctor FOREIGN KEY (id_doctor) REFERENCES Doctores(id_doctor),
    CONSTRAINT FK_HistorialDoctores_Paciente FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente)
);




SELECT * FROM Pacientes;
SELECT * FROM Doctores;
SELECT * FROM Citas;


SELECT Citas.id_cita, Pacientes.nombre AS Paciente, Doctores.nombre AS Doctor, Citas.fecha_hora, Citas.estado
FROM Citas
JOIN Pacientes ON Citas.id_paciente = Pacientes.id_paciente
JOIN Doctores ON Citas.id_doctor = Doctores.id_doctor;
GO

SELECT 
    p.nombre AS Paciente,
    d.nombre AS Doctor,
    c.fecha_hora,
    c.estado
FROM Citas c
JOIN Pacientes p ON c.id_paciente = p.id_paciente
JOIN Doctores d ON c.id_doctor = d.id_doctor
WHERE c.estado = 'Confirmada';
GO












