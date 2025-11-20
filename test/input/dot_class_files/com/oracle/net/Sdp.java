/*
 * Decompiled with CFR 0.152.
 * 
 * Could not load the following classes:
 *  com.oracle.net.Sdp$SdpSocket
 *  sun.nio.ch.Secrets
 */
package com.oracle.net;

import com.oracle.net.Sdp;
import java.io.FileDescriptor;
import java.io.IOException;
import java.lang.reflect.AccessibleObject;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketImpl;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.security.AccessController;
import sun.net.sdp.SdpSupport;
import sun.nio.ch.Secrets;

public final class Sdp {
    private static final Constructor<ServerSocket> serverSocketCtor;
    private static final Constructor<SocketImpl> socketImplCtor;

    private Sdp() {
    }

    private static void setAccessible(AccessibleObject o) {
        AccessController.doPrivileged(new /* Unavailable Anonymous Inner Class!! */);
    }

    private static SocketImpl createSocketImpl() {
        try {
            return socketImplCtor.newInstance(new Object[0]);
        }
        catch (InstantiationException x) {
            throw new AssertionError((Object)x);
        }
        catch (IllegalAccessException x) {
            throw new AssertionError((Object)x);
        }
        catch (InvocationTargetException x) {
            throw new AssertionError((Object)x);
        }
    }

    public static Socket openSocket() throws IOException {
        SocketImpl impl = Sdp.createSocketImpl();
        return new SdpSocket(impl);
    }

    public static ServerSocket openServerSocket() throws IOException {
        SocketImpl impl = Sdp.createSocketImpl();
        try {
            return serverSocketCtor.newInstance(impl);
        }
        catch (IllegalAccessException x) {
            throw new AssertionError((Object)x);
        }
        catch (InstantiationException x) {
            throw new AssertionError((Object)x);
        }
        catch (InvocationTargetException x) {
            Throwable cause = x.getCause();
            if (cause instanceof IOException) {
                throw (IOException)cause;
            }
            if (cause instanceof RuntimeException) {
                throw (RuntimeException)cause;
            }
            throw new RuntimeException(x);
        }
    }

    public static SocketChannel openSocketChannel() throws IOException {
        FileDescriptor fd = SdpSupport.createSocket();
        return Secrets.newSocketChannel((FileDescriptor)fd);
    }

    public static ServerSocketChannel openServerSocketChannel() throws IOException {
        FileDescriptor fd = SdpSupport.createSocket();
        return Secrets.newServerSocketChannel((FileDescriptor)fd);
    }

    static {
        try {
            serverSocketCtor = ServerSocket.class.getDeclaredConstructor(SocketImpl.class);
            Sdp.setAccessible(serverSocketCtor);
        }
        catch (NoSuchMethodException e) {
            throw new AssertionError((Object)e);
        }
        try {
            Class<?> cl = Class.forName("java.net.SdpSocketImpl", true, null);
            socketImplCtor = cl.getDeclaredConstructor(new Class[0]);
            Sdp.setAccessible(socketImplCtor);
        }
        catch (ClassNotFoundException e) {
            throw new AssertionError((Object)e);
        }
        catch (NoSuchMethodException e) {
            throw new AssertionError((Object)e);
        }
    }
}
